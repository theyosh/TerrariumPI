<%@ page import="java.lang.*"%>
<%@ page import="java.sql.*"%>
<%@ page import="com.google.gson.*"%>
<%
	// database connection
	// "jdbc:mysql://localhost:3306/northwind" - the database url of the form jdbc:subprotocol:subname
	// "root" - the database user on whose behalf the connection is being made
	// "abcd" - the user's password
	Connection dbConnection = DriverManager.getConnection(
			"jdbc:mysql://localhost:3306/northwind", "root", "abcd");

	// retrieve necessary records from database
	Statement getFromDb = dbConnection.createStatement();
	ResultSet employees = getFromDb
			.executeQuery("SELECT FirstName, Title FROM employees");

	// format returned ResultSet as a JSON array
	JsonArray recordsArray = new JsonArray();
	while (employees.next()) {
		JsonObject currentRecord = new JsonObject();
		currentRecord.add("FirstName",
				new JsonPrimitive(employees.getString("FirstName")));
		currentRecord.add("Title",
				new JsonPrimitive(employees.getString("Title")));
		recordsArray.add(currentRecord);
	}
	out.print(recordsArray);
	out.flush();
%>