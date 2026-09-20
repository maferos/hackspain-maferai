// One id and successful request per document load, including StrictMode mounts.
const session = crypto.randomUUID();
let request;

// With a seed (from ?seed=N) the backend loads that catalogue pattern instead
// of a random one; the same seed the viewport label shows.
export function chooseScene(backendUrl, seed) {
  if (!request) {
    const seedParam = seed != null && seed !== "" ? `&seed=${encodeURIComponent(seed)}` : "";
    request = fetch(`${backendUrl}/api/scene/randomize?session=${session}${seedParam}`, {
      method: "POST",
    }).then(async (response) => {
      if (!response.ok) throw new Error("Scene selection unavailable");
      return response.json();
    }).catch((error) => {
      request = null;
      throw error;
    });
  }
  return request;
}
