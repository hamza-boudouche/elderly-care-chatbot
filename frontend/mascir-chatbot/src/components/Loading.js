import React from "react";
import loading from "../assets/loading.svg";

const Loading = () => (
	<div className="spinner" style={{
		width: "100%",
		height: "100%",
		display: "grid",
		justifyContent: "center",
		alignItems: "center"
	}}>
		<img src={loading} alt="Loading" />
	</div>
);

export default Loading;
