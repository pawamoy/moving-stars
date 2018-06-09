#!/bin/bash
sort -u mapping_data.json | tail -n+3 > /tmp/moving_stars_mapping_data || exit 1
{
  echo [
  cat /tmp/moving_stars_mapping_data
  echo ]
} > mapping_data.json
