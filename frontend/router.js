import { writable } from 'svelte/store';

export const currentRoute = writable(window.location.hash.slice(1) || '/');

window.addEventListener('hashchange', () => {
  currentRoute.set(window.location.hash.slice(1) || '/');
});

export function navigate(path) {
    console.log("Router:" +path)
  window.location.hash = path;
}