<script>
  import { enhance } from '$app/forms';

  let loading = false;

  function handleSubmit() {
    loading = true;
    // Form submission is handled by the server
  }
</script>

<div class="min-h-screen bg-coffee-cream bg-texture-paper py-16 px-4">
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

  .text-shadow {
    text-shadow: 1px 1px 2px rgba(120, 108, 59, 0.1);
  }
</style>