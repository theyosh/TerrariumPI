<%@ page import="java.lang.*"%>
<%@ page import="java.sql.*"%>
<%@ page import="com.google.gson.*"%>
<%
	String itemValue = request.getParameter("widget");
	out.print(itemValue);
	out.flush();
%>