<%@ page import="java.lang.*"%>
<%@ page import="java.sql.*"%>
<%@ page import="com.google.gson.*"%>
<%
	String category = request.getParameter("category");

	// database connection
	// "jdbc:mysql://localhost:3306/northwind" - the database url of the form jdbc:subprotocol:subname
	// "root" - the database user on whose behalf the connection is being made
	// "abcd" - the user's password
	Connection dbConnection = DriverManager.getConnection(
			"jdbc:mysql://localhost:3306/northwind", "root", "abcd");

	// retrieve necessary records from database
	Statement getFromDb = dbConnection.createStatement();
	ResultSet products = getFromDb
			.executeQuery("SELECT ProductName, UnitsInStock FROM products WHERE CategoryID="
					+ category);

	// format returned ResultSet as a JSON array
	JsonArray recordsArray = new JsonArray();
	while (products.next()) {
		JsonObject currentRecord = new JsonObject();
		currentRecord.add("ProductName",
				new JsonPrimitive(products.getString("ProductName")));
		currentRecord.add("UnitsInStock",
				new JsonPrimitive(products.getString("UnitsInStock")));
		recordsArray.add(currentRecord);
	}
	out.print(recordsArray);
	out.flush();
%>