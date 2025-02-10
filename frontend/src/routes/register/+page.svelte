<script>
  import { enhance } from '$app/forms';

  let loading = false;
  let password = '';
  let confirmPassword = '';
  let passwordsMatch = true;

  $: passwordsMatch = !confirmPassword || password === confirmPassword;

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
        Join the Table
      </h1>
      <p class="text-lg text-coffee-medium font-garamond italic">
        Start your coffee journey with us
      </p>
    </div>

    <!-- Registration Form -->
    <form 
      method="POST" 
      use:enhance={handleSubmit}
      class="bg-white rounded-xl shadow-warm border border-coffee-light/20 p-8"
    >
      <div class="space-y-6">
        <!-- Username -->
        <div>
          <label for="username" class="block font-garamond text-lg text-coffee-deep mb-2">
            Username
          </label>
          <input
            type="text"
            name="username"
            id="username"
            required
            class="input w-full"
            placeholder="Your preferred username"
          />
        </div>

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
            bind:value={password}
            class="input w-full"
            placeholder="Choose a secure password"
          />
        </div>

        <!-- Confirm Password -->
        <div>
          <label for="confirmPassword" class="block font-garamond text-lg text-coffee-deep mb-2">
            Confirm Password
          </label>
          <input
            type="password"
            id="confirmPassword"
            required
            bind:value={confirmPassword}
            class="input w-full"
            class:border-coffee-burgundy={!passwordsMatch}
            placeholder="Confirm your password"
          />
          {#if !passwordsMatch}
            <p class="mt-2 text-sm text-coffee-burgundy">
              Passwords don't match
            </p>
          {/if}
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          disabled={loading || !passwordsMatch}
          class="w-full px-8 py-3 rounded-lg bg-coffee-deep text-coffee-cream font-medium 
                 shadow-md transition-all duration-300 ease-out transform 
                 hover:scale-102 hover:shadow-lg hover:bg-coffee-medium
                 border border-coffee-gold/20 text-lg
                 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? 'Creating Account...' : 'Create Account'}
        </button>

        <!-- Sign In Link -->
        <div class="text-center mt-6">
          <a 
            href="/login"
            class="text-coffee-medium hover:text-coffee-deep transition-colors duration-200"
          >
            Already have an account? Sign in
          </a>
        </div>
      </div>
    </form>

    <!-- Additional Info -->
    <div class="mt-8 text-center text-coffee-medium text-sm">
      <p>
        By creating an account, you agree to share your coffee journey with fellow enthusiasts.
      </p>
    </div>
  </div>
</div>