---
title: First notebook (in R)
params:
  out_file: NULL
---

```R name="setup"
library(ggplot2)
library(dplyr)
library(readr)
```

# A plot.
```R
ggplot(iris, aes(x=Sepal.Width, y=Sepal.Length, color=Species)) +
  geom_point() +
  theme_bw()
```

# Export data
```R message=false
write_tsv(iris, params$out_file)
```


