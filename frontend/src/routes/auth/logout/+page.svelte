<script lang="ts">
  import { onMount } from 'svelte';
  
  let message = 'Logging out...';
  
  onMount(() => {
    const form = document.getElementById('logoutForm') as HTMLFormElement;
    if (form) {
      form.submit();
    }
  });
</script>

<div class="fixed inset-0 bg-coffee-deep/95 backdrop-blur-sm z-50 flex items-center justify-center">
  <div class="text-center space-y-4">
    <!-- Spinner -->
    <div class="inline-block">
      <div class="w-12 h-12 rounded-full border-4 border-coffee-cream/20 border-t-coffee-gold animate-spin"></div>
    </div>
    
    <!-- Message -->
    <p class="text-coffee-cream font-garamond text-xl">{message}</p>
  </div>
</div>

<!-- Hidden form that will be auto-submitted -->
<form 
  id="logoutForm"
  method="POST" 
  class="hidden"
>
</form>
