package com.nato.c2;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface TrackRepository extends JpaRepository<TrackEntity, Long> {

    List<TrackEntity> findByClassification(String classification);

    @Query(value = "SELECT * FROM asset_tracks WHERE classification = 'HOSTILE' ORDER BY recorded_at DESC LIMIT 50", nativeQuery = true)
    List<TrackEntity> findRecentHostileTracks();

    @Query(value = "SELECT DISTINCT ON (track_id) * FROM asset_tracks ORDER BY track_id, recorded_at DESC", nativeQuery = true)
    List<TrackEntity> findLatestTracksForAllAssets();
}