import { clearStoredUser, getStoredUser, storeUser } from "./session";

describe("session storage helpers", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  test("stores and retrieves user data", () => {
    const user = { id: 1, username: "rahul", full_name: "Rahul Kumar" };

    storeUser(user);

    expect(getStoredUser()).toEqual(user);
  });

  test("clears stored user data", () => {
    storeUser({ id: 2, username: "sneha" });

    clearStoredUser();

    expect(getStoredUser()).toBeNull();
  });

  test("returns null for invalid stored payload", () => {
    window.localStorage.setItem("scholarsync-user", "{bad-json");

    expect(getStoredUser()).toBeNull();
  });
});
