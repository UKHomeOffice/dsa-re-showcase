import React from "react";
import "./Catalogue.css";
import unicorn1 from "../../assets/images/unicorn-catalogue.png";

const Catalogue = () => {
  const products = [
    {
      id: 1,
      name: "Unicorn 1",
      image: unicorn1,
      description: "A reliable unicorn.",
    },
    {
      id: 2,
      name: "Unicorn 2",
      image: unicorn1,
      description: "An efficient unicorn.",
    },
  ];

  return (
    <div className="catalogue-container">
      <h1>Unicorn Catalogue</h1>
      <div className="catalogue-grid">
        {products.map((product) => (
          <div key={product.id} className="catalogue-item">
            <img src={product.image} alt={product.name} />
            <h2>{product.name}</h2>
            <p>{product.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Catalogue;
