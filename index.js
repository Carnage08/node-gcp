const express = require("express");
const { Storage } = require("@google-cloud/storage");
const path = require("path");

const app = express();
const storage = new Storage();

const BUCKET_NAME = "gcloude_01";

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "public", "form.html"));
});

app.post("/submit", async (req, res) => {
  try {
    console.log("Submit route hit");
    console.log(req.body);

    const { name, email, contact, branch, position } = req.body;

    if (!name || !email || !contact || !branch || !position) {
      return res.status(400).send("Missing required fields");
    }

    const timestamp = new Date().toISOString();

    const bucket = storage.bucket(BUCKET_NAME);
    const fileName = `responses/form_${Date.now()}.csv`;
    const file = bucket.file(fileName);

    const safe = (val) =>
      String(val || "").replace(/,/g, " ").replace(/\n/g, " ");

    const csvData =
      "name,email,contact,branch,position,timestamp\n" +
      `${safe(name)},${safe(email)},${safe(contact)},${safe(branch)},${safe(position)},${timestamp}\n`;

    await file.save(csvData, {
      contentType: "text/csv",
    });

    console.log("File saved:", fileName);

    res.status(200).send("Saved");

  } catch (error) {
    console.error("FULL ERROR:", error);
    res.status(500).send("Internal Server Error");
  }
});

const PORT = 3000;

app.listen(PORT, "0.0.0.0", () => {
  console.log(`Server running on port ${PORT}`);
});
