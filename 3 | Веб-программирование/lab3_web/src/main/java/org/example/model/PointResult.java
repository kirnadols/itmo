package org.example.model;

import jakarta.persistence.*;
import org.example.HashUtil;
import java.io.Serializable;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

@Entity
@Table(name = "results")
public class PointResult implements Serializable {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private Double x;
    private Double y;
    private Double r;
    private boolean result;

    @Column(name = "query_time")
    private String queryTime;

    // --- БЛОКЧЕЙН ПОЛЯ ---
    @Column(name = "prev_hash")
    private String previousHash;

    @Column(name = "curr_hash")
    private String currentHash;

    public PointResult() {}

    public PointResult(Double x, Double y, Double r, boolean result, String previousHash) {
        this.x = x;
        this.y = y;
        this.r = r;
        this.result = result;
        this.queryTime = LocalDateTime.now().format(DateTimeFormatter.ofPattern("dd.MM.yyyy HH:mm:ss"));

        this.previousHash = previousHash;
        this.currentHash = calculateHash();
    }

    public String calculateHash() {
        String rawData = x + "" + y + "" + r + "" + result + "" + queryTime + "" + previousHash;
        return HashUtil.sha256(rawData);
    }

    public Long getId() { return id; }
    public Double getX() { return x; }
    public Double getY() { return y; }
    public Double getR() { return r; }
    public boolean isResult() { return result; }
    public String getQueryTime() { return queryTime; }
    public String getResultString() { return result ? "Попадание" : "Промах"; }
    public String getPreviousHash() { return previousHash; }
    public String getCurrentHash() { return currentHash; }
}