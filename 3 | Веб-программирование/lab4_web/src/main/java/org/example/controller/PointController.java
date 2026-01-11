package org.example.controller;

import org.example.dto.PointRequest;
import org.example.entity.Point;
import org.example.entity.User;
import org.example.repository.PointRepository;
import org.example.repository.UserRepository;
import org.example.service.AreaCheckService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.security.Principal;
import java.time.LocalDateTime;
import java.util.List;

@RestController
@RequestMapping("/api/points")
public class PointController {
    private final PointRepository pointRepository;
    private final UserRepository userRepository;
    private final AreaCheckService areaCheckService;

    public PointController(PointRepository pointRepository, UserRepository userRepository,
                           AreaCheckService areaCheckService) {
        this.pointRepository = pointRepository;
        this.userRepository = userRepository;
        this.areaCheckService = areaCheckService;
    }

    @GetMapping
    public List<Point> getPoints(Principal principal) {
        User user = userRepository.findByUsername(principal.getName()).orElseThrow();
        return pointRepository.findAllByUser(user);
    }

    @PostMapping
    public ResponseEntity<?> addPoint(@RequestBody PointRequest request, Principal principal) {
        if (request.getR() <= 0) {
            return ResponseEntity.badRequest().body("R must be positive");
        }

        User user = userRepository.findByUsername(principal.getName()).orElseThrow();

        boolean isHit = areaCheckService.checkHit(request.getX(), request.getY(), request.getR());

        Point point = new Point();
        point.setX(request.getX());
        point.setY(request.getY());
        point.setR(request.getR());
        point.setResult(isHit);
        point.setCheckedAt(LocalDateTime.now());
        point.setUser(user);

        return ResponseEntity.ok(pointRepository.save(point));
    }
}