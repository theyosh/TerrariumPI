<%@ page import="java.lang.*"%>
<%@ page import="java.sql.*"%>
<%@ page import="com.google.gson.*"%>
<%
	String rowToDelete = request.getParameter("row");

	//database connection
	// "jdbc:mysql://localhost:3306/northwind" - the database url of the form jdbc:subprotocol:subname
	// "root" - the database user on whose behalf the connection is being made
	// "abcd" - the user's password
	Connection dbConnection = DriverManager.getConnection(
			"jdbc:mysql://localhost:3306/northwind", "root", "abcd");

	// delete specified record from the database
	Statement deleteFromDb = dbConnection.createStatement();
	int delete = deleteFromDb
			.executeUpdate("DELETE FROM employees WHERE EmployeeID="
					+ rowToDelete);
%>