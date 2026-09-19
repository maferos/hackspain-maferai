// One id and successful request per document load, including StrictMode mounts.
const session = crypto.randomUUID();
let request;

export function chooseScene(backendUrl) {
  if (!request) {
    request = fetch(`${backendUrl}/api/scene/randomize?session=${session}`, {
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
