library(stringr)
througput_table <- function(data_frame, delta){
  
  #seleziono l'elenco dei job ID
  job_id <- unique(data_frame$Job_ID)
  
  # converto i timestamp in timestamp unix
  data_frame$Timestamp = as.numeric(as.POSIXct(data_frame$Timestamp))
  
  tmp_df <- matrix(nrow= 0, ncol=2)
  colnames(tmp_df) <- c("TS", "Job_ID")
  
  
  # seleziono il timestamp più grande delle righe con lo stesso JOB_ID 
  for(job in job_id){
    data <- data_frame[grepl(job, data_frame$Job_ID), ]
    tmp_df <- rbind(tmp_df, c(as.numeric(max(data$Timestamp)), job))
  }
  
  tmp_df <- as.data.frame(tmp_df)
  tmp_df$TS <- as.double(as.character(tmp_df$TS))
  
  # prendo il min timestamp da cui contare ogni x secondi il num di pacchetti processati
  
  # delta = 15
  start_ts = min(tmp_df$TS)
  
  current_ts = start_ts
  end_ts = max(tmp_df[,1])
  
  result <- matrix(nrow= 0, ncol=2)
  colnames(result) <- c("TS", "Throughout")
  
  while(current_ts < end_ts){
    row_selected = tmp_df[which(tmp_df$TS >= current_ts &
                                tmp_df$TS < current_ts+ delta,
                                arr.ind = TRUE),] 
    
    
    result <-rbind(result, c(current_ts, NROW(row_selected) / delta))
    
    current_ts = current_ts + delta
  }
  
  return(result)
  
}

create_df <- function(file_name){
  
  df <- read.csv( file= file_name, header = T, stringsAsFactors = F,sep=",")
  
  df <- data.frame(df$X.timestamp, str_split_fixed(df$X.message, ", RequestId:", 2))
  colnames(df) <- c("Timestamp", "Job_ID", "Request_ID")
  return(df)
  
}
file_name = "thr_100.csv"
file_1 = "./data/thr_100_notify.csv"
file_2 = "./data/thr_100_eventProcessor.csv"
file_3 = "./data/thr_100_checkFall.csv"
file_4 = "./data/thr_100_checkPosition.csv"
file_5 = "./data/thr_100_checkHeartRate.csv"


file_out = paste0("./out/", file_name)

t1 <- create_df(file_1)
t2 <- create_df(file_2)
t3 <- create_df(file_3)
t4 <- create_df(file_4)
t5 <- create_df(file_5)

all_data <- rbind(t1, t2, t3, t4, t5)

data <- througput_table(all_data, delta= 15)# delta in secondi

write.csv(data , file_out)

