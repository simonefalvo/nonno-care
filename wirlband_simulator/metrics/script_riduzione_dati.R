' Script aggregazione dati per graficarli '

aggregate_data <- function(file_name, delta){
  
  data <- df_notify <- read.csv(  
    file= file_name,
    header = T,
    stringsAsFactors = F,
    sep=",")
  
  data <- data[order(data$TS),]
  
  #ora che i dati sono ordinati per ts il ts iniziale e' il primo
  start_ts = data$TS[1]
  end_ts = max(data$TS)
  current_ts = start_ts
  
  
  result <- matrix(nrow= 0, ncol=2)
  colnames(result) <- c("TS", "Duration")
  
  while(current_ts <= end_ts){
    row_selected = data[which(data$TS >= current_ts &
                              data$TS < current_ts + delta, arr.ind = TRUE),] 
    
    if(nrow(row_selected)!= 0){
      result <-rbind(result, c(current_ts, mean(row_selected$Duration)))  
    }
    
    
    current_ts = current_ts + delta
  }
  
  return(result)
  
}

file_name <- "./data_out/lat_1000.csv"


out_data <- aggregate_data(file_name, delta=5)
write.csv(out_data , "./data_out/lat_1000_reduced.csv")

