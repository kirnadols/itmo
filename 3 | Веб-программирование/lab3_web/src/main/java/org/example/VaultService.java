package org.example;

import jakarta.enterprise.context.ApplicationScoped;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

@ApplicationScoped
public class VaultService {
    private static final String VAULT_URL = "http://127.0.0.1:8200/v1/secret/data/lab3_merkle";
    private static final String VAULT_TOKEN = "root";

    public void saveRoot(String rootHash) {
        try {
            String json = String.format("{\"data\": {\"root\": \"%s\"}}", rootHash);

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create(VAULT_URL))
                    .header("X-Vault-Token", VAULT_TOKEN)
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(json))
                    .build();

            HttpClient.newHttpClient().sendAsync(request, HttpResponse.BodyHandlers.ofString());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}