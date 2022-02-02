const server = "http://127.0.0.1:3579";

describe("Basic form submission", () => {
  it("Visits the home page", () => {
    cy.visit("/");

    cy.get("input[name=name]")
      .type("Some Random Name")
      .should("have.value", "Some Random Name");

    cy.intercept("POST", `${server}/datasets/`).as("new-dataset");
    cy.get("button").click().contains("loading...");
    cy.wait("@new-dataset").should(({ request, response }) => {
      expect(request.method).to.equal("POST");
      expect(response.statusCode).to.equal(200);
    });
  });
});
