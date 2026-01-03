package org.example.servlets;

import org.example.model.Point;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

@WebServlet("/check")
public class AreaCheckServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        try {
            double x = Double.parseDouble(req.getParameter("x").replace(",", "."));
            double y = Double.parseDouble(req.getParameter("y").replace(",", "."));
            double r = Double.parseDouble(req.getParameter("r").replace(",", "."));

            if (!checkOpa(x, y, r)) {
                resp.sendRedirect("index.jsp?error=opa_ban");
                return;
            }

            boolean isHit = checkArea(x, y, r);

            Point point = new Point(x, y, r, isHit);

            HttpSession session = req.getSession();
            List<Point> history = (List<Point>) session.getAttribute("history");
            if (history == null) {
                history = new ArrayList<>();
            }
            history.add(0, point);
            session.setAttribute("history", history);

            resp.sendRedirect("result.jsp");

        } catch (NumberFormatException | NullPointerException e) {
            resp.sendRedirect("index.jsp");
        } catch (Exception e) {
            e.printStackTrace();
            resp.sendRedirect("index.jsp");
        }
    }

    private boolean checkOpa(double x, double y, double r) {
        try {
            String jsonBody = String.format(
                    "{\"input\": {\"x\": %s, \"y\": %s, \"r\": %s}}",
                    String.valueOf(x), String.valueOf(y), String.valueOf(r)
            );

            HttpClient client = HttpClient.newBuilder()
                    .connectTimeout(Duration.ofSeconds(1))
                    .build();

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("http://localhost:8190/v1/data/lab2/allow"))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            return response.body() != null && response.body().contains("\"result\":true");

        } catch (Exception e) {
            System.err.println("OPA Warning: Сервер политик недоступен (" + e.getMessage() + "). Разрешаем по умолчанию.");
            return true;
        }
    }

    private boolean checkArea(double x, double y, double r) {
        if (x >= 0 && y >= 0) {
            return (x * x + y * y) <= Math.pow(r / 2.0, 2);
        }

        if (x <= 0 && y >= 0) {
            return (x >= -r) && (y <= r);
        }

        if (x <= 0 && y <= 0) {
            return y >= (-0.5 * x - r / 2.0);
        }

        return false;
    }
}