import React, {useState} from "react";
import {submitResearch, getTasks} from "../api";

export default function ResearchForm(){
  const [query, setQuery] = useState("");
  const [urls, setUrls] = useState("https://example.com");
  const [message, setMessage] = useState(null);

  const onSubmit = async (e) => {
    e.preventDefault();
    const start_urls = urls.split("\n").map(u => u.trim()).filter(Boolean);
    const res = await submitResearch(query, start_urls);
    setMessage(JSON.stringify(res));
  };

  return (
    <div style={{padding:20}}>
      <h2>DeepResearch — quick demo</h2>
      <form onSubmit={onSubmit}>
        <div>
          <label>Query</label><br/>
          <input value={query} onChange={e=>setQuery(e.target.value)} style={{width:500}} />
        </div>
        <div>
          <label>Start URLs (one per line)</label><br/>
          <textarea value={urls} onChange={e=>setUrls(e.target.value)} rows={6} cols={80}/>
        </div>
        <button type="submit">Start Research</button>
      </form>
      <div style={{marginTop:20}}>{message}</div>
    </div>
  );
}
