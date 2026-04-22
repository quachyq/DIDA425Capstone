library(sf)
library(tidyverse)
library(leaflet)
library(spData)
library(htmlwidgets)

datacenter_sf = read_sf("static/data/datacenters.shp") %>% select(c(fclty_n, oprtr_n,sizernk,prjct_c,status))

datacenter_sf[is.na(datacenter_sf)] = "Unknown"

p_popup = paste0("<b>Facility Name: </b>", datacenter_sf$fclty_n, 
                 "<br>",
                 "<b>Operator: </b>", datacenter_sf$oprtr_n, 
                 "<br>",
                 "<b>Size Rank: </b>", datacenter_sf$sizernk, 
                 "<br>",
                 "<b>Projected Cost: </b>",datacenter_sf$prjct_c, sep = "")

my_colors = c(
  "Approved/Permitted/Under construction" = "green",
  "Cancelled" = "red",
  "Expanding" = "coral",
  "Operating" = "blue",
  "Proposed" = "orange",
  "Suspended" = "darkgoldenrod",
  "Unknown" = "purple"
)
pal_fun = colorFactor(my_colors, datacenter_sf$status)

map = leaflet() %>% onRender("
    function(el, x) {
      this.on('popupopen', function(e) {
        console.log(e.popup.getContent());
      });
    }
  ") %>%
  addCircleMarkers(data = datacenter_sf, color = ~pal_fun(status), radius = 1,
          popup = p_popup) %>%
  addProviderTiles(providers$CartoDB.Positron) %>%
  addLegend("bottomright",  # location
          pal=pal_fun,    # palette function
          values=datacenter_sf$status, 
          title = 'Status') # legend

saveWidget(map, file = "templates/map_widget.html", selfcontained = T)

