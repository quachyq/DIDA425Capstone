library(sf)
library(tidyverse)
library(leaflet)
library(spData) 
library(urbnmapr)

states <- get_urbn_map("states", sf = TRUE)

states <- states %>% 
  st_transform("EPSG:4326")

datacenter_sf = read_sf("static/data/datacenters.shp")

pal_fun = colorFactor(topo.colors(3), datacenter_sf$status)

leaflet() %>%
  addCircleMarkers(data = datacenter_sf, color = ~pal_fun(status), radius = 1) %>%
  addProviderTiles(providers$CartoDB.Positron) %>%
  addLegend("bottomright",  # location
          pal=pal_fun,    # palette function
          values=datacenter_sf$status, 
          title = 'Status') # legend 
