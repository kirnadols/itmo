package org.example;

import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

class Params {
    private final double x;
    private final double y;
    private final double r;

    private static final List<Double> VALID_X_VALUES = List.of(-4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0);
    private static final double MIN_Y = -5.0;
    private static final double MAX_Y = 5.0;
    private static final List<Double> VALID_R_VALUES = List.of(1.0, 1.5, 2.0, 2.5, 3.0);

    public Params(String query) throws ValidationException {
        if (query == null || query.isEmpty()) {
            throw new ValidationException("Request body is empty.");
        }
        Map<String, String> params = parseQuery(query);

        this.x = validateAndParseDouble(params.get("x"), "X", VALID_X_VALUES);
        this.y = validateAndParseDouble(params.get("y"), "Y", MIN_Y, MAX_Y);
        this.r = validateAndParseDouble(params.get("r"), "R", VALID_R_VALUES);
    }

    private Map<String, String> parseQuery(String query) {
        return Arrays.stream(query.split("&"))
                .map(pair -> pair.split("=", 2))
                .filter(parts -> parts.length == 2)
                .collect(Collectors.toMap(
                        parts -> URLDecoder.decode(parts[0], StandardCharsets.UTF_8),
                        parts -> URLDecoder.decode(parts[1], StandardCharsets.UTF_8)
                ));
    }

    private double validateAndParseDouble(String value, String name, List<Double> validValues) throws ValidationException {
        if (value == null || value.isEmpty()) {
            throw new ValidationException(String.format("Parameter '%s' is missing.", name));
        }
        try {
            double parsedValue = Double.parseDouble(value.replace(",", "."));
            if (!validValues.contains(parsedValue)) {
                throw new ValidationException(String.format("Value for '%s' is not allowed. Got: %f.", name, parsedValue));
            }
            return parsedValue;
        } catch (NumberFormatException e) {
            throw new ValidationException(String.format("Parameter '%s' must be a number.", name));
        }
    }

    private double validateAndParseDouble(String value, String name, double min, double max) throws ValidationException {
        if (value == null || value.isEmpty()) {
            throw new ValidationException(String.format("Parameter '%s' is missing.", name));
        }
        try {
            double parsedValue = Double.parseDouble(value.replace(",", "."));
            if (parsedValue <= min || parsedValue >= max) {
                throw new ValidationException(String.format("Value for '%s' must be in range (%f, %f).", name, min, max));
            }
            return parsedValue;
        } catch (NumberFormatException e) {
            throw new ValidationException(String.format("Parameter '%s' must be a number.", name));
        }
    }

    public double getX() { return x; }
    public double getY() { return y; }
    public double getR() { return r; }
}