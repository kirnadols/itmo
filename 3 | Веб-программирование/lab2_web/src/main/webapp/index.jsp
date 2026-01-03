<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<%@ page import="java.util.List" %>
<%@ page import="org.example.model.Point" %>
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Лабораторная работа №2</title>
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/main.css">

    <script>
        const historyPoints = [
            <%
            List<Point> history = (List<Point>) session.getAttribute("history");
            if (history != null) {
                for (Point p : history) {
            %>
                { x: <%= p.getX() %>, y: <%= p.getY() %>, r: <%= p.getR() %>, hit: <%= p.isHit() %> },
            <%
                }
            }
            %>
        ];
    </script>
</head>
<body>

<header>
    <h1>Надольский Кирилл Николаевич</h1>
    <p>Группа: P3209 | Вариант: 466824</p>
</header>

<main>

    <%
        String errorType = request.getParameter("error");
        if ("opa_ban".equals(errorType)) {
    %>
        <div class="opa-alert">
            <h3>⛔ Доступ запрещен политикой безопасности ⛔</h3>
            <p>Система OPA (Open Policy Agent) заблокировала ваш запрос.</p>
            <p style="font-size: 0.9em; margin-top: 5px;">Причина: Обнаружены запрещенные числовые комбинации</p>
        </div>
    <% } %>

    <%
        Point lastPoint = null;
        if (history != null && !history.isEmpty()) {
            lastPoint = history.get(0);
        }
        // Показываем плашку, только если это не редирект с ошибкой
        if (lastPoint != null && errorType == null) {
    %>
        <div class="result-notification <%= lastPoint.isHit() ? "hit-true" : "hit-false" %>"
             style="margin-bottom: 20px; text-align: center; padding: 10px; border: 1px solid; border-radius: 5px;">
            <h3>
                Результат последнего выстрела:
                <%= lastPoint.isHit() ? "ПОПАДАНИЕ" : "ПРОМАХ" %>
            </h3>
        </div>
    <% } %>

    <section class="content-area">
        <div class="graph-container">
            <h2>Область на координатной плоскости</h2>
            <canvas id="graphCanvas" width="300" height="300"></canvas>
        </div>

        <div class="form-container">
            <h2>Параметры для проверки</h2>
            <p id="error-message" class="error"></p>

            <form id="shot-form" action="controller" method="GET" onsubmit="return validateForm()">

                <div class="form-group">
                    <label>Значение X</label>
                    <div class="radio-group">
                        <% for(int i=-3; i<=5; i++) { %>
                            <label><input type="radio" name="x" value="<%=i%>"> <%=i%></label>
                        <% } %>
                    </div>
                </div>

                <div class="form-group">
                    <label for="y-value">Значение Y (от -3 до 5)</label>
                    <input type="text" id="y-value" name="y" placeholder="например, 1.23">
                </div>

                <div class="form-group">
                    <label for="r-value">Значение R (от 2 до 5)</label>
                    <input type="text" id="r-value" name="r"
                           placeholder="например, 3"
                           oninput="drawGraph()"
                           value="<%= request.getParameter("r") == null ? "" : request.getParameter("r") %>">
                </div>

                <div class="form-actions">
                    <button type="submit" class="submit-btn">Проверить</button>
                </div>
            </form>
        </div>
    </section>

    <section class="results-area">
        <h2>История проверок</h2>
        <div class="table-wrapper">
            <table>
                <thead>
                <tr>
                    <th>X</th>
                    <th>Y</th>
                    <th>R</th>
                    <th>Результат</th>
                    <th>Время</th>
                </tr>
                </thead>
                <tbody>
                <%
                    if (history != null) {
                        for (Point p : history) {
                %>
                <tr>
                    <td><%= p.getX() %></td>
                    <td><%= p.getY() %></td>
                    <td><%= p.getR() %></td>
                    <td class="<%= p.isHit() ? "hit-true" : "hit-false" %>">
                        <%= p.isHit() ? "Попадание" : "Промах" %>
                    </td>
                    <td><%= p.getTime() %></td>
                </tr>
                <%      }
                    }
                %>
                </tbody>
            </table>
        </div>
    </section>
</main>

<script src="js/script.js"></script>
</body>
</html>