import { useEffect, useState } from "react";

const url = "http://localhost:8000";

// Helper function to handle JSON responses
async function fetchJson(url: string, options: RequestInit = {}) {
  const response = await fetch(url, options);
  return response.json();
}

// Authentication functions
async function login(username: string) {
  const data = new FormData();
  data.append("username", username);
  data.append("password", "123");

  const response = await fetchJson(url + "/token", {
    method: "POST",
    body: data,
  });
  return response.access_token;
}

// File upload functions
async function onUpload(file: File, token: string) {
  const data = new FormData();
  data.append("file", file);

  return fetchJson(url + "/upload", {
    method: "POST",
    body: data,
    headers: { Authorization: `Bearer ${token}` },
  });
}

// Function to toggle public/private status
async function onSetPublic(id: string, token: string) {
  return fetchJson(url + `/set-public?id=${id}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
}

// Retrieve images function
async function fetchImages(token: string) {
  return fetchJson(url + "/images", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

// Get token from local storage
function getToken() {
  return localStorage.getItem("token");
}

function App() {
  const [token, setToken] = useState<string | null>(getToken());
  const [username, setUsername] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(true);
  const [images, setImages] = useState<
    { is_public: boolean; filename: string; id: string; user: string }[]
  >([]);

  // Initial token and loading state check
  useEffect(() => {
    if (token) {
      fetchImages(token).then(setImages);
    }
    setLoading(false);
  }, [token]);

  const handleLogin = async () => {
    const token = await login(username);
    if (token) {
      setToken(token);
      localStorage.setItem("token", token);
    }
  };

  const handleUpload = async () => {
    if (!file || !token) return;
    const uploadedData = await onUpload(file, token);
    setImages([...images, uploadedData]);
  };

  const handleTogglePublic = async (id: string, index: number) => {
    if (!token) return;
    await onSetPublic(id, token);
    const updatedImages = [...images];
    updatedImages[index].is_public = !updatedImages[index].is_public;
    setImages(updatedImages);
  };

  if (loading) {
    return (
      <h1 className="flex justify-center items-center h-screen text-2xl">
        Loading ...
      </h1>
    );
  }

  return (
    <div className="flex flex-col items-center h-screen space-y-5">
      {token ? (
        <>
          <div className="flex items-center gap-x-5">
            <h1>Logged in as: {token}</h1>
            <button
              onClick={() => {
                localStorage.removeItem("token");
                setToken(null);
              }}
              className="bg-red-500 py-2 px-5 text-white rounded active:scale-95"
            >
              Logout
            </button>
          </div>

          <div className="grid gap-5 w-full max-w-xl mx-auto">
            {images.map((image, index) => (
              <div key={image.id}>
                <div className="w-40 h-40 overflow-hidden border rounded p-2">
                  <h1>{image.user}</h1>
                  <img
                    src={`http://localhost:8000/static/${image.filename}`}
                    alt={image.filename}
                    className="rounded w-full object-cover h-full"
                  />
                </div>
                {token === image.user && (
                  <button
                    className={`px-2 py-1 ${
                      image.is_public ? "text-red-500" : "text-blue-500"
                    }`}
                    onClick={() => handleTogglePublic(image.id, index)}
                  >
                    {image.is_public ? "Private" : "Public"}
                  </button>
                )}
              </div>
            ))}
          </div>

          <div className="mt-10">
            <label>Select file to share</label>
            <br />
            <input type="file" onChange={(e) => setFile(e.target.files![0])} />
            <button
              className="bg-blue-500 rounded text-white px-4 py-2 active:scale-95"
              onClick={handleUpload}
            >
              Upload
            </button>
          </div>
        </>
      ) : (
        <div className="flex flex-col justify-center items-center h-screen space-y-2">
          <label htmlFor="username" className="text-slate-500">
            Example:
            <br />
            - johndoe
            <br />- alice
          </label>
          <input
            id="username"
            type="text"
            className="border py-2 px-4 rounded outline-none focus:border-blue-500"
            placeholder="Username..."
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <button
            className="bg-blue-500 rounded text-white px-4 py-2 active:scale-95"
            onClick={handleLogin}
          >
            Login
          </button>
        </div>
      )}
    </div>
  );
}

export default App;
