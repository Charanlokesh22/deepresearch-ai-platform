import axios from "axios";
const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000/api";

export async function submitResearch(query, start_urls){
  const resp = await axios.post(`${API_BASE}/research`, {query, start_urls});
  return resp.data;
}

export async function getTasks(){
  const resp = await axios.get(`${API_BASE}/tasks`);
  return resp.data;
}

export async function getReport(uid){
  const resp = await axios.get(`${API_BASE}/report/${uid}`);
  return resp.data;
}
