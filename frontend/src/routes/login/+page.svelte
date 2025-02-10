<script>
  import { enhance } from '$app/forms';

  let loading = false;

  function handleSubmit() {
    loading = true;
    // Form submission is handled by the server
  }
</script>

<div class="min-h-screen bg-texture py-16 px-4">
  <div class="max-w-md mx-auto">
    <!-- Header -->
    <div class="text-center mb-12">
      <h1 class="text-4xl font-garamond font-medium text-coffee-deep mb-4 text-shadow">
        Welcome Back
      </h1>
      <p class="text-lg text-coffee-medium font-garamond italic">
        il tuo tavolo ti aspetta
      </p>
    </div>

    <!-- Login Form -->
    <form 
      method="POST" 
      use:enhance={handleSubmit}
      class="bg-white rounded-xl shadow-warm border border-coffee-light/20 p-8"
    >
      <div class="space-y-6">
        <!-- Email -->
        <div>
          <label for="email" class="block font-garamond text-lg text-coffee-deep mb-2">
            Email
          </label>
          <input
            type="email"
            name="email"
            id="email"
            required
            class="input w-full"
            placeholder="your@email.com"
          />
        </div>

        <!-- Password -->
        <div>
          <label for="password" class="block font-garamond text-lg text-coffee-deep mb-2">
            Password
          </label>
          <input
            type="password"
            name="password"
            id="password"
            required
            class="input w-full"
            placeholder="Enter your password"
          />
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          disabled={loading}
          class="w-full px-8 py-3 rounded-lg bg-coffee-deep text-coffee-cream font-medium 
                 shadow-md transition-all duration-300 ease-out transform 
                 hover:scale-102 hover:shadow-lg hover:bg-coffee-medium
                 border border-coffee-gold/20 text-lg
                 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Signing In...' : 'Sign In'}
        </button>

        <!-- Register Link -->
        <div class="text-center mt-6">
          <a 
            href="/register"
            class="text-coffee-medium hover:text-coffee-deep transition-colors duration-200"
          >
            Need an account? Join the table
          </a>
        </div>
      </div>
    </form>

    <!-- Additional Info -->
    <div class="mt-8 text-center text-coffee-medium text-sm">
      <p>
        Your coffee journey continues here
      </p>
    </div>
  </div>
</div>

<style>
  .input {
    @apply px-4 py-2 rounded-lg border border-coffee-light/30 
           focus:border-coffee-gold/50 focus:ring-2 focus:ring-coffee-gold/20 
           outline-none transition-all duration-200
           placeholder:text-coffee-medium/50;
  }

  .bg-texture {
    background-color: #f8f4e9;
    background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M11 18c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm48 25c3.866 0 7-3.134 7-7s-3.134-7-7-7-7 3.134-7 7 3.134 7 7 7zm-43-7c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm63 31c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM34 90c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zm56-76c1.657 0 3-1.343 3-3s-1.343-3-3-3-3 1.343-3 3 1.343 3 3 3zM12 86c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm28-65c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm23-11c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-6 60c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm29 22c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zM32 63c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm57-13c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm-9-21c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM60 91c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM35 41c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2zM12 60c1.105 0 2-.895 2-2s-.895-2-2-2-2 .895-2 2 .895 2 2 2z' fill='%23786c3b' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E");
  }

  .text-shadow {
    text-shadow: 1px 1px 2px rgba(120, 108, 59, 0.1);
  }
</style>