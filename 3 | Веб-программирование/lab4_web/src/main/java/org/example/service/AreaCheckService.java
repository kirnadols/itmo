package org.example.service;

import org.springframework.stereotype.Service;

@Service
public class AreaCheckService {

    public boolean checkHit(double x, double y, double r) {
        if (r <= 0) return false;

        if (x >= 0 && y >= 0) {
            return x <= r && y <= r;
        }

        if (x <= 0 && y >= 0) {
            return (x * x + 4 * y * y) <= (r * r);
        }

        if (x <= 0 && y <= 0) {
            return y >= (-2 * x - r);
        }

        return false;
    }
}