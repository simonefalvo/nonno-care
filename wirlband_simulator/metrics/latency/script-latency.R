
library("dplyr")


list_job_id <- function(job_df){
  
  start_pos <- 7
  end_pos <-gregexpr(pattern = ',', job_df$X.message) 
  
  # elenco dei job_id
  jobs_id <- substr(job_df$X.message, start_pos, end_pos)
  
  return(jobs_id)
}

list_request_id <- function(job_df){
  # calcola la posizione del terminatore del req_id
  start_pos <- gregexpr(pattern = 'RequestId: ', job_df$X.message) 
  
  # elenco dei req_id
  reqs_id <- substr(job_df$X.message, start_pos, nchar(job_df$X.message)-1) # remove \n
  
  return(reqs_id)
}


generate_table <- function(file_name){
  
  df <- read.csv(  
    file= file_name,
    header = T,
    stringsAsFactors = F,
    sep=",")
  
  
  # converto i timestamp in timestamp unix
  df$X.timestamp = as.numeric(as.POSIXct(df$X.timestamp))
  
  result_df <- matrix(nrow=0, ncol = 4)
  
  #seleziona i messaggi di inizio, ovvero i JOBID
  job_df <- df[grepl("JOB_ID", df[["X.message"]]), ]
  
  # elenco dei job_id
  jobs_id <- list_job_id(job_df)
  
  # elenco dei req_id
  reqs_id <- list_request_id(job_df)
  
  #seleziona i messaggi di fine, ovvero i REPORT
  report_df <- df[grepl("REPORT RequestId:", df[["X.message"]]), ]
  
  
  i <- 1
  
  # ricavo req_id e durata per il job_id
  for(request in reqs_id){
    
    # seleziono la riga di interesse
    row <- report_df[grepl(request, report_df[["X.message"]]), ]
    
    # TODO: se piu di una riga errore
    if(nrow(row) > 1){
      cat("Numero di righe maggiore di 1 pari a: ")
      cat(nrow(row))
      
    }
    ts <- row[1,1]
    row <- row[1,2]
    
    # start duratioon
    start = gregexpr(pattern = '\tDuration:', row)
    end = gregexpr(pattern = 'ms\tBilled Duration', row)
    duration = substr(row, start[[1]][1] + 11, end[[1]][1] -2)
    
    
    # trovo la riga della matrice di risultato associata a cui dare la durata
    
    result_df <- rbind(result_df, c(as.integer(ts), jobs_id[i], request, as.double(duration)))
    i <- i + 1
    
  } 
  
  return(result_df)
}

save_in_one_file <-function(all_data, file_out){
  all_data <- as.data.frame(all_data)
  colnames(all_data) <- c("TS", "Job_ID", "Duration")
  
  all_data$Duration <- as.double(as.character(all_data$Duration))
  all_data <- data.frame(lapply(all_data, as.character), stringsAsFactors=FALSE)
  all_data$Duration <- as.double(as.character(all_data$Duration))
  
  
  # somma le latenze degli stessi Job_ID e mantiene TS più grande
  
  file_result <- matrix(nrow= 0, ncol=3)
  colnames(file_result) <- c("TS", "Job_ID", "Duration")
  
  job_id <- all_data$Job_ID
  job_id <- unique(job_id)
  
  for(job in job_id){
    
    data <- all_data[grepl(job, all_data$Job_ID), ]
    file_result <- rbind(file_result, c(max(data$TS), job, sum(data$Duration)))
    
  }
  
  write.csv(file_result, file_out)
  return(file_result)
}




file_name = "lat_500.csv"
file_in = paste0("./data/", file_name)
file_out = paste0("./out/", file_name)

t1 <- generate_table("./data/lat_500_notify.csv")
t2 <- generate_table("./data/lat_500_checkFall.csv")
t3 <- generate_table("./data/lat_500_checkHeartRate.csv")
t4 <- generate_table("./data/lat_500_checkPosition.csv")
t5 <- generate_table("./data/lat_500_eventProcessor.csv")


#all_data <- t1
all_data <- rbind(t1, t2,t4, t5)
all_data <- all_data[,-3] #rimuovo la colonna dei request-id non mi serve piu 

save_in_one_file(all_data, file_out)
