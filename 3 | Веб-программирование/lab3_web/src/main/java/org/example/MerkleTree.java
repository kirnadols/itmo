package org.example;

import org.example.HashUtil;
import java.util.ArrayList;
import java.util.List;

public class MerkleTree {
    private List<String> leaves;
    private String root;

    public MerkleTree(List<String> leaves) {
        this.leaves = leaves;
        this.root = buildRoot(leaves);
    }

    private String buildRoot(List<String> hashes) {
        if (hashes.isEmpty()) return "";
        if (hashes.size() == 1) return hashes.get(0);

        List<String> nextLevel = new ArrayList<>();
        for (int i = 0; i < hashes.size(); i += 2) {
            String left = hashes.get(i);
            String right = (i + 1 < hashes.size()) ? hashes.get(i + 1) : left;
            nextLevel.add(HashUtil.sha256(left + right));
        }
        return buildRoot(nextLevel);
    }

    public String getRoot() { return root; }

    public List<String> getProof(String leafHash) {
        List<String> proof = new ArrayList<>();
        int index = leaves.indexOf(leafHash);
        if (index == -1) return proof;

        List<String> currentLevel = new ArrayList<>(leaves);
        while (currentLevel.size() > 1) {
            List<String> nextLevel = new ArrayList<>();
            for (int i = 0; i < currentLevel.size(); i += 2) {
                String left = currentLevel.get(i);
                String right = (i + 1 < currentLevel.size()) ? currentLevel.get(i + 1) : left;

                if (i == index || i + 1 == index) {
                    proof.add((i == index) ? right : left);
                    index = i / 2;
                }
                nextLevel.add(HashUtil.sha256(left + right));
            }
            currentLevel = nextLevel;
        }
        return proof;
    }
}