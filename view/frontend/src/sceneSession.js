// One id and successful request per document load, including StrictMode mounts.
const session = crypto.randomUUID();
let request;

// With ?scene=N, select catalogue scene p01 through p04 by number.
export function chooseScene(backendUrl, sceneNumber) {
  if (!request) {
    const sceneParam = sceneNumber != null && sceneNumber !== "" ? `&scene=${encodeURIComponent(sceneNumber)}` : "";
    request = fetch(`${backendUrl}/api/scene/randomize?session=${session}${sceneParam}`, {
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
