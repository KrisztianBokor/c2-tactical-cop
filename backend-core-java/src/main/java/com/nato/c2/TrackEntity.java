package com.nato.c2;

import jakarta.persistence.*;
import org.locationtech.jts.geom.Point;
import java.math.BigDecimal;
import java.time.OffsetDateTime;

@Entity
@Table(name = "asset_tracks")
public class TrackEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "track_id", nullable = false, length = 32)
    private String trackId;

    @Column(name = "classification", nullable = false, length = 16)
    private String classification;

    @Column(name = "speed_knots", precision = 6, scale = 2)
    private BigDecimal speedKnots;

    @Column(name = "altitude_m", precision = 8, scale = 2)
    private BigDecimal altitudeM;

    @Column(name = "heading_deg", precision = 5, scale = 2)
    private BigDecimal headingDeg;

    @Column(name = "location", columnDefinition = "geometry(Point,4326)", nullable = false)
    private Point location;

    @Column(name = "recorded_at")
    private OffsetDateTime recordedAt;

    public Long getId() { return id; }
    public String getTrackId() { return trackId; }
    public String getClassification() { return classification; }
    public BigDecimal getSpeedKnots() { return speedKnots; }
    public BigDecimal getAltitudeM() { return altitudeM; }
    public BigDecimal getHeadingDeg() { return headingDeg; }
    public Point getLocation() { return location; }
    public OffsetDateTime getRecordedAt() { return recordedAt; }
}