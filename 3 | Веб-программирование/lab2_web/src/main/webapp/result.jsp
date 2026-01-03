<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="org.example.model.Point" %>
<%@ page import="java.util.List" %>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Результат проверки</title>
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/main.css">
</head>
<body>

<header>
    <h1>Результат проверки</h1>
    <p>Лабораторная работа №2</p>
</header>

<main>
    <section class="content-area" style="justify-content: center;">
        <div class="form-container" style="max-width: 600px; flex: none; text-align: center;">

            <%
                List<Point> history = (List<Point>) session.getAttribute("history");
                Point p = null;
                if (history != null && !history.isEmpty()) {
                    p = history.get(0);
                }

                if (p != null) {
            %>

            <h2 style="margin-bottom: 20px;">
                Результат:
                <span class="<%= p.isHit() ? "hit-true" : "hit-false" %>" style="font-size: 1.2em;">
                    <%= p.isHit() ? "ПОПАДАНИЕ" : "ПРОМАХ" %>
                </span>
            </h2>

            <div class="table-wrapper">
                <table style="margin: 0 auto;">
                    <thead>
                        <tr>
                            <th>Параметр X</th>
                            <th>Параметр Y</th>
                            <th>Радиус R</th>
                            <th>Время</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><%= p.getX() %></td>
                            <td><%= p.getY() %></td>
                            <td><%= p.getR() %></td>
                            <td><%= p.getTime() %></td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <% } else { %>
                <p class="error">Нет данных для отображения. Сделайте проверку на главной странице.</p>
            <% } %>

            <div style="margin-top: 30px;">
                <a href="index.jsp" style="text-decoration: none;">
                    <button class="submit-btn" style="width: auto; padding: 10px 30px;">
                        Вернуться назад
                    </button>
                </a>
            </div>

        </div>
    </section>
</main>

</body>
</html>