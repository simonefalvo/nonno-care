
generate_table <- function(file_name){
  
  df <- read.csv(  
    file= file_name,
    header = T,
    stringsAsFactors = F,
    sep=",")
  
  
  # converto i timestamp in timestamp unix
  df$X.timestamp = as.numeric(as.POSIXct(df$X.timestamp))
  
  result_df <- matrix(nrow=0, ncol = 3)
  
  #seleziona i messaggi di inizio, ovvero i JOBID
  job_df <- df[grepl("JOB_ID", df[["X.message"]]), ]
  
  # calcola la posizione del terminatore del Job_id
  start_pos <- 7
  end_pos <-gregexpr(pattern = ',', job_df$X.message) 
  
  # elenco dei job_id
  jobs_id <- substr(job_df$X.message, start_pos, end_pos)
  
  # calcola la posizione del terminatore del req_id
  start_pos <- gregexpr(pattern = 'RequestId: ', job_df$X.message) 
  
  # elenco dei req_id
  reqs_id <- substr(job_df$X.message, start_pos, nchar(job_df$X.message)-1) # remove \n
  
  
  
  
  
  #seleziona i messaggi di fine, ovvero i JOBID
  report_df <- df[grepl("REPORT RequestId:", df[["X.message"]]), ]
  
  
  i <- 1
  
  # ricavo req_id e durata per il job_id
  for(request in reqs_id){
    request <- reqs_id[i]
    # seleziono la riga di interesse
    row <- report_df[grepl(request, report_df[["X.message"]]), ]
    # TODO: se piu di una riga errore
    if(nrow(row) > 1){
      cat("Numero di righe maggiore di 1 pari a: ")
      cat(nrow(row))
      
    }
    row <- row[1,2]
    
    # start duratioon
    start = gregexpr(pattern = '\tDuration:', row)
    end = gregexpr(pattern = 'ms\tBilled Duration', row)
    duration = substr(row, start[[1]][1] + 11, end[[1]][1] -2)
    
    
   
    result_df <- rbind(result_df, c(jobs_id[i], request, as.double(duration)))
    i <- i + 1
    
  }
  
  return(result_df)
}

t1 <- generate_table("./latency/logs-insights-results-check-position.csv")
t2 <- generate_table("./latency/logs-insights-results-heart.csv")

all_data <- rbind(t1, t2)

all_data <- all_data[,-2] 


all_data <- as.data.frame(all_data)

all_data$V2 <- as.double(as.character(all_data$V2))
all_data <- data.frame(lapply(all_data, as.character), stringsAsFactors=FALSE)
all_data$V2 <- as.double(as.character(all_data$V2))

# agg contiene la somma delle durate dei corrispettivi Job_id
agg = aggregate(all_data[-1],
                by = lista,
                FUN = sum)
