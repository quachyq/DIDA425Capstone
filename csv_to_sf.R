library(sf)

datacenter_df = read.csv("datacenters.csv")

datacenter_sf = st_as_sf(datacenter_df, coords = c("long","lat"), crs = 4326, remove = F)

st_write(datacenter_sf, "static/data/datacenters.shp", delete_layer = T)

