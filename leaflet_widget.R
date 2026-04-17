library(sf)
library(tidyverse)
library(leaflet)
library(spData)
library(htmlwidgets)

datacenter_sf = read_sf("static/data/datacenters.shp") %>% select(c(fclty_n, oprtr_n,sizernk,prjct_c,status))

datacenter_sf[is.na(datacenter_sf)] = ""

p_popup = paste0("Facility Name: ", datacenter_sf$fclty_n, 
                 "<br>",
                 "Operator: ", datacenter_sf$oprtr_n, 
                 "<br>",
                 "Size Rank: ", datacenter_sf$sizernk, 
                 "<br>",
                 "Projected Cost: ",datacenter_sf$prjct_c, sep = "")

pal_fun = colorFactor(topo.colors(3), datacenter_sf$status)

map = leaflet() %>%
  addCircleMarkers(data = datacenter_sf, color = ~pal_fun(status), radius = 1,
          popup = p_popup) %>%
  addProviderTiles(providers$CartoDB.Positron) %>%
  addLegend("bottomright",  # location
          pal=pal_fun,    # palette function
          values=datacenter_sf$status, 
          title = 'Status') # legend 

saveWidget(map, file = "map_widget.html", selfcontained = T)

