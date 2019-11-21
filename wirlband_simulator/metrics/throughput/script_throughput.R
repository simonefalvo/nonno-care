
througput_table <- function(file_name, delta){
  res <- df_notify <- read.csv(  
    file= file_name,
    header = T,
    stringsAsFactors = F,
    sep=",")
  
  # converto i timestamp in timestamp unix
  res$X.timestamp = as.numeric(as.POSIXct(res$X.timestamp))
  
  # seleziono il timestamp più grande delle righe con lo stesso messageid 
  agg = aggregate(res,
                  by = list(res$X.message),
                  FUN = max)
  
  # prendo il min timestamp da cui contare ogni x secondi il num di pacchetti processati
  
  # delta = 15
  start_ts = min(agg$X.timestamp)
  
  current_ts = start_ts
  end_ts = max(agg$X.timestamp)
  
  result <- matrix(nrow= 0, ncol=2)
  colnames(result) <- c("TS", "N Execution")
  
  while(current_ts < end_ts){
    row_selected = agg[which(agg$X.timestamp >= current_ts &
                               agg$X.timestamp < current_ts+ delta, arr.ind = TRUE),] 
    
    
    result <-rbind(result, c(current_ts, NROW(row_selected)))
    
    current_ts = current_ts + delta
  }
  
  return(result)
  
}
file_name = "thr_100_notify.csv"
file_in = paste0("./data/", file_name)
file_out = paste0("./out/", file_name)

data = througput_table(file_in, delta= 15)# delta in secondi

write.csv(data , file_out)

