package org.example;

import com.fastcgi.FCGIInterface;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoUnit;
import java.util.Locale;

public class Main {

    private static final DateTimeFormatter dtf = DateTimeFormatter.ofPattern("HH:mm:ss dd.MM.yyyy");

    private static final String HTTP_RESPONSE = """
            Status: 200 OK
            Content-Type: application/json
            Content-Length: %d

            %s""";
    private static final String HTTP_ERROR = """
            Status: 400 Bad Request
            Content-Type: application/json
            Content-Length: %d

            %s""";

    private static final String RESULT_JSON_ENTRY = """
            {"x": %s, "y": %s, "r": %s, "time": "%s", "now": "%s", "result": %b%s}""";

    private static final String DEBUG_JSON_ENTRY = """
        , "debug": {
            "validationTimeNs": %d,
            "calcTimeNs": %d,
            "memoryUsedBytes": %d,
            "threadId": %d
        }""";

    private static final String ERROR_JSON = """
            {
                "now": "%s",
                "reason": "%s"
            }""";

    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        var fcgi = new FCGIInterface();
        while (fcgi.FCGIaccept() >= 0) {
            try {
                String queryString = System.getProperty("QUERY_STRING");
                String debugToken = System.getProperty("HTTP_X_DEBUG_TOKEN");

                boolean isDebugMode = "true".equals(parseQueryParam(queryString, "debug"))
                        && "secret".equals(debugToken);

                String requestMethod = System.getProperty("REQUEST_METHOD");
                if (!"POST".equals(requestMethod)) {
                    throw new ValidationException("This endpoint only supports POST requests. Received: " + (requestMethod != null ? requestMethod : "null"));
                }

                String requestBody = "";
                String contentLengthStr = System.getProperty("CONTENT_LENGTH");

                if (contentLengthStr != null && !contentLengthStr.isEmpty()) {
                    int contentLength = Integer.parseInt(contentLengthStr);
                    if (contentLength > 0) {
                        try (BufferedReader reader = new BufferedReader(
                                new InputStreamReader(System.in, StandardCharsets.UTF_8))) {
                            char[] buffer = new char[contentLength];
                            reader.read(buffer, 0, contentLength);
                            requestBody = new String(buffer);
                        }
                    }
                }

                Instant validationStartTime = Instant.now();
                var params = new Params(requestBody);
                Instant validationEndTime = Instant.now();

                Instant calcStartTime = Instant.now();
                var result = calculate(params.getX(), params.getY(), params.getR());
                Instant calcEndTime = Instant.now();

                long validationTime = ChronoUnit.NANOS.between(validationStartTime, validationEndTime);
                long calcTime = ChronoUnit.NANOS.between(calcStartTime, calcEndTime);
                long totalTime = ChronoUnit.NANOS.between(validationStartTime, calcEndTime);

                String debugJson = "";
                if (isDebugMode) {
                    Runtime runtime = Runtime.getRuntime();
                    long memoryUsed = runtime.totalMemory() - runtime.freeMemory();
                    long threadId = Thread.currentThread().getId();

                    debugJson = String.format(DEBUG_JSON_ENTRY,
                            validationTime,
                            calcTime,
                            memoryUsed,
                            threadId
                    );
                }

                String newResultJson = String.format(RESULT_JSON_ENTRY,
                        params.getX(),
                        params.getY(),
                        params.getR(),
                        totalTime,
                        dtf.format(LocalDateTime.now()),
                        result,
                        debugJson
                );

                var response = String.format(HTTP_RESPONSE,
                        newResultJson.getBytes(StandardCharsets.UTF_8).length,
                        newResultJson
                );
                System.out.print(response);

            } catch (ValidationException e) {
                var json = String.format(ERROR_JSON, dtf.format(LocalDateTime.now()), e.getMessage());
                var response = String.format(HTTP_ERROR, json.getBytes(StandardCharsets.UTF_8).length, json);
                System.out.print(response);
            } catch (Exception e) {
                e.printStackTrace(System.err);
                var json = String.format(ERROR_JSON, dtf.format(LocalDateTime.now()), "Server Error: " + e.getMessage());
                var response = String.format(HTTP_ERROR, json.getBytes(StandardCharsets.UTF_8).length, json);
                System.out.print(response);
            }
        }
    }

    private static String parseQueryParam(String query, String paramName) {
        if (query == null || query.isEmpty()) return null;
        for (String pair : query.split("&")) {
            String[] parts = pair.split("=", 2);
            if (parts.length == 2 && parts[0].equals(paramName)) {
                try {
                    return URLDecoder.decode(parts[1], StandardCharsets.UTF_8.name());
                } catch (UnsupportedEncodingException e) {
                    return null;
                }
            }
        }
        return null;
    }

    private static boolean calculate(double x, double y, double r) {

        if (x >= 0 && y >= 0) {
            return y <= (-x / 2) + (r / 2);
        }

        if (x < 0 && y >= 0) {
            return (x >= -r) && (y <= r / 2);
        }

        if (x <= 0 && y < 0) {
            return (x * x + y * y) <= (r / 2) * (r / 2);
        }

        if (x > 0 && y < 0) {
            return false;
        }

        return false;
    }
}