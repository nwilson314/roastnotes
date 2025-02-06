<script>
    let user = { name: 'Nate', bio: 'coffee enthusiast', profilePic: '/path/to/pic.jpg' };
  </script>
  
  <div class="profile-page">
    <div class="profile-card">
      <img src={user.profilePic} alt="Profile Pic" class="profile-pic" />
      <h2>{user.name}</h2>
      <p>{user.bio}</p>
    </div>
  </div>
  
  <style>
    .profile-page {
      display: flex;
      justify-content: center;
      padding: 2rem;
    }
    .profile-card {
      border: 1px solid #ddd;
      padding: 2rem;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      text-align: center;
    }
    .profile-pic {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      object-fit: cover;
      margin-bottom: 1rem;
    }
  </style>
  