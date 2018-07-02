#!/bin/bash
unset LANG
sort -u src/moving_stars/mapping_data.toml | head -n-2 > /tmp/moving_stars_mapping_data || exit 1
{
  echo data = [
  cat /tmp/moving_stars_mapping_data
  echo ]
} > mapping_data.toml
