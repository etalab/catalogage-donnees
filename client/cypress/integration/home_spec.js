const server = "http://127.0.0.1:3579";

describe("Basic form submission", () => {
  it("Visits the home page", () => {
    const title = "Un nom de jeu de données";
    const description = "Une longue\ndescription de jeu\nde données";
    cy.visit("/");

    cy.get("#title").type(title).should("have.value", title);
    cy.get("#description").type(description).should("have.value", description);

    cy.intercept("POST", `${server}/datasets/`).as("new-dataset");
    cy.get("button").click().contains("loading...");
    cy.wait("@new-dataset").should(({ request, response }) => {
      expect(request.method).to.equal("POST");
      expect(response.statusCode).to.equal(201);
      expect(response.body.title).to.equal(title);
      expect(response.body.description).to.equal(description);
      expect(response.body).to.have.property("id");
    });
  });
});
