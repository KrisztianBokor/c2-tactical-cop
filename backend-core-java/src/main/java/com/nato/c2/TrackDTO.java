package com.nato.c2;

import java.math.BigDecimal;

public record TrackDTO(
    String id,
    String classification,
    Double lat,
    Double lon,
    BigDecimal speed,
    BigDecimal altitude,
    BigDecimal heading,
    String timestamp
) {}