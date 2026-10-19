package com.nato.c2;

import org.springframework.web.bind.annotation.*;
import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/v1/c2")
@CrossOrigin(origins = "*")
public class TrackController {

    private final TrackRepository trackRepository;

    public TrackController(TrackRepository trackRepository) {
        this.trackRepository = trackRepository;
    }

    @GetMapping("/cop/latest")
    public List<TrackDTO> getLatestCOP() {
        return trackRepository.findLatestTracksForAllAssets().stream().map(track -> new TrackDTO(
            track.getTrackId(),
            track.getClassification(),
            track.getLocation() != null ? track.getLocation().getY() : null,
            track.getLocation() != null ? track.getLocation().getX() : null,
            track.getSpeedKnots(),
            track.getAltitudeM(),
            track.getHeadingDeg(),
            track.getRecordedAt() != null ? track.getRecordedAt().toString() : null
        )).collect(Collectors.toList());
    }

    @GetMapping("/alerts/hostile")
    public List<TrackEntity> getHostileAlerts() {
        return trackRepository.findRecentHostileTracks();
    }
}