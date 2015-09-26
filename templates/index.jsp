<html>
<body>

<form action="" method=POST>{% csrf_token %}
	<fieldset>
		<legend>Git Repository Issue Details</legend>
		  *Enter Github Url:
		  <input type="text" name="url" width="500px"><br><br>
		  <input type="submit" value="Submit" onclick='alert();'><br>
		  <p class="required">* Required</p>
	</fieldset>

	<fieldset>
	<legend> Result </legend>
		Error : {{message}}<br>
		<p1>UserName :</p1>  {{user}}<br>
		<p1>Repository Name :</p1>  {{repo}}<br>
		<br>Total Open Issues :  {{total}}
		<br>Total Issues Opened in Last 24 Hrs :  {{within1}}
		<br>Total Issues created in last 7 days and befor 24Hrs :  {{within7}}
		<br>Total Issues created before 7 days :  {{before7}}
		  
	</fieldset>

<script>
function alert() {
   alert("Please Wait for the result to process");
}
</script> 

</form>
</body>
</html>
