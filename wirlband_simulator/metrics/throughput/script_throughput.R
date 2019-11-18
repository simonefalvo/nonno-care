
df_battiti <- read.csv(  
  file= './throughput/logs-insights-results-battiti.csv',
  header = T,
  stringsAsFactors = F,
  sep=",")


df_caduta <- read.csv(  
  file= './throughput/logs-insights-results-caduta.csv',
  header = T,
  stringsAsFactors = F,
  sep=",")


df_position <- read.csv(  
  file= './throughput/logs-insights-results-check-position.csv',
  header = T,
  stringsAsFactors = F,
  sep=",")


df_notify <- read.csv(  
  file= './throughput/logs-insights-results-notify.csv',
  header = T,
  stringsAsFactors = F,
  sep=",")

# aggrego i dati in un unico dataframe
res <- rbind(df_position, df_notify,
             df_caduta, df_battiti)

res <- df_notify <- read.csv(  
  file= './throughput/logs-insights-results-checkposition-100-1440.csv',
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
delta = 15
start_ts = min(agg$X.timestamp)
current_ts = start_ts
end_ts = max(agg$X.timestamp)
value_graph <- c()
ts <- c()

  while(current_ts < end_ts){
    row_selected = agg[which(agg$X.timestamp >= current_ts &
                         agg$X.timestamp < current_ts+ delta, arr.ind = TRUE),] 
    
    
    value_graph <- c(value_graph, NROW(row_selected))
    ts <- c(ts, current_ts)
    current_ts = current_ts + delta
}


plot(ts,value_graph, type="l") 


