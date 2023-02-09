export const Readexcel = () => {
  const handleSubmit = (event) => {
    event.preventDefault();

    const data = new FormData();
    data.append("conversion", "excel_json");
    data.append("delimiter", ";");
    data.append("file", document.querySelector("#fileinput").files[0]);

    const options = {
      method: "POST",
      headers: {
        "X-RapidAPI-Key": "1ed3d7ac68msh584657b52a77c8ep1b6ee0jsnc9d4c619e627",
        "X-RapidAPI-Host": "file-converter2.p.rapidapi.com",
      },
      body: data,
    };

    fetch("https://file-converter2.p.rapidapi.com/convert/", options)
      .then((response) => response.json())
      .then((res) => res.map((obj) => obj.Contact))
      .then((res) => res.join(","))
      .then((res) => (document.querySelector("#numberinput-excel").value = res))
      .then(() => document.querySelector("#numberinput-excel").focus())
      .then(() => document.querySelector("#closebtn").click())
      .catch((err) => console.error(err));
  };

  return (
    <form onSubmit={handleSubmit}>
      <input id="fileinput" type="file" />
      <button type="submit">업로드</button>
    </form>
  );
};
