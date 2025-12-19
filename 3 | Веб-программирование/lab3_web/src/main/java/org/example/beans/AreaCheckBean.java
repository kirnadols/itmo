package org.example.beans;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.enterprise.context.SessionScoped;
import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.persistence.*;
import org.example.MerkleTree;
import org.example.VaultService;
import org.example.model.PointResult;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

@Named("areaCheckBean")
@SessionScoped
public class AreaCheckBean implements Serializable {

    private Double x = 0.0;
    private Double y = 0.0;
    private Double r = 1.0;
    private List<PointResult> results = new ArrayList<>();

    private EntityManagerFactory emf;
    private EntityManager em;

    @Inject
    private VaultService vaultService;

    @PostConstruct
    public void init() {
        try {
            emf = Persistence.createEntityManagerFactory("LabUnit");
            em = emf.createEntityManager();
            loadHistory();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void loadHistory() {
        if (em != null) {
            try {
                results = em.createQuery("SELECT p FROM PointResult p ORDER BY p.id DESC", PointResult.class).getResultList();
            } catch (Exception e) {
                e.printStackTrace();
                results = new ArrayList<>();
            }
        }
    }

    public void checkPoint() {
        boolean hit = checkArea(x, y, r);

        String prevHash = "00000000000000000000000000000000";
        if (!results.isEmpty()) {
            prevHash = results.get(0).getCurrentHash();
        }

        PointResult resultEntity = new PointResult(x, y, r, hit, prevHash);

        if (em != null) {
            try {
                em.getTransaction().begin();
                em.persist(resultEntity);
                em.getTransaction().commit();

                results.add(0, resultEntity);

                updateAuditSystem();

            } catch (Exception e) {
                if (em.getTransaction().isActive()) em.getTransaction().rollback();
                e.printStackTrace();
            }
        }
    }

    private void updateAuditSystem() {
        try {
            List<String> allHashes = em.createQuery("SELECT p.currentHash FROM PointResult p ORDER BY p.id ASC", String.class).getResultList();

            if (!allHashes.isEmpty()) {
                MerkleTree tree = new MerkleTree(allHashes);
                String root = tree.getRoot();
                vaultService.saveRoot(root);
                System.out.println("Merkle Root updated: " + root);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public String getProof(PointResult p) {
        try {
            List<String> allHashes = em.createQuery("SELECT p.currentHash FROM PointResult p ORDER BY p.id ASC", String.class).getResultList();
            MerkleTree tree = new MerkleTree(allHashes);
            return tree.getProof(p.getCurrentHash()).toString();
        } catch (Exception e) {
            return "[]";
        }
    }

    public String getJsonResults() {
        if (results == null || results.isEmpty()) {
            return "[]";
        }
        StringBuilder json = new StringBuilder("[");
        for (int i = 0; i < results.size(); i++) {
            PointResult p = results.get(i);
            json.append(String.format(Locale.US,
                    "{\"x\":%s, \"y\":%s, \"result\":%b}",
                    p.getX(), p.getY(), p.isResult()));

            if (i < results.size() - 1) {
                json.append(",");
            }
        }
        json.append("]");
        return json.toString();
    }

    public void setJsonResults(String jsonResults) {
    }

    private boolean checkArea(Double x, Double y, Double r) {
        if (r == null || r <= 0) return false;
        if (x >= 0 && y >= 0) return (x <= r / 2.0) && (y <= r);
        if (x <= 0 && y >= 0) return (x * x + y * y) <= (r * r);
        if (x <= 0 && y <= 0) return y >= (-x - r / 2.0);
        return false;
    }

    @PreDestroy
    public void destroy() {
        if (em != null && em.isOpen()) em.close();
        if (emf != null && emf.isOpen()) emf.close();
    }

    public Double getX() { return x; }
    public void setX(Double x) { this.x = x; }
    public Double getY() { return y; }
    public void setY(Double y) { this.y = y; }
    public Double getR() { return r; }
    public void setR(Double r) { this.r = r; }
    public List<PointResult> getResults() { return results; }
}