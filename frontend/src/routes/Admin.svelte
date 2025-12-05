<script>
    async function add_user() {
        const response = await fetch('http://127.0.0.1:8000/api/v1/users/', {method:'POST'});
    }
</script>

<h1>Admin Page</h1>

<form id="addUserForm" action="http://127.0.0.1:8000/api/v1/users/" method="POST">
    <h2>Add User</h2>
    <div>
        <input class="adminInput" type="text" id="username" name="username" placeholder="Username..." />
        <input class="adminInput" type="email" id="email" name="email" placeholder="Email address..." />
        <input class="adminInput" type="password" id="password" name="password" placeholder="Password..." />
    </div>
    <button type="submit">+ Add User</button>
</form>

<p>Click <a href="https://github.com/JD0ud/JDoudCOS243Proj2" target="_blank">here</a> to access the GitHub repository.</p>