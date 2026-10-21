import { test, expect } from "@playwright/test";
import type { Page } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

async function ready(page: Page) {
  await page.goto("/");
  await expect(page.getByText("Ready for your question")).toBeVisible();
}

test("desktop onboarding, keyboard controls and no broken assets", async ({
  page,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (error) => errors.push(error.message));
  page.on("response", (response) => {
    if (response.status() >= 400)
      errors.push(`${response.status()} ${response.url()}`);
  });
  await page.setViewportSize({ width: 1440, height: 1000 });
  await ready(page);
  await expect(page).toHaveTitle("Scout — Education, continued.");
  await expect(
    page.getByRole("heading", { name: "Big changes. Small steps forward." }),
  ).toBeVisible();
  await expect(
    page
      .getByRole("region", { name: "Ways Scout can help" })
      .getByRole("button"),
  ).toHaveCount(6);
  expect(
    (await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze())
      .violations,
  ).toEqual([]);
  await page.getByRole("button", { name: /Replace lost documents/ }).click();
  await expect(page.getByLabel("Your message to Scout")).toBeFocused();
  await expect(page.getByLabel("Your message to Scout")).toHaveValue(
    /transfer certificate/,
  );
  await page.getByLabel("Your message to Scout").fill("");
  await expect(
    page.getByRole("button", { name: "Send message" }),
  ).toBeDisabled();
  await page.screenshot({
    path: "../artifacts/scout-desktop.png",
    fullPage: true,
  });
  expect(errors).toEqual([]);
});

test("mobile navigation is usable and the page does not overflow", async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await ready(page);
  expect(
    (await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze())
      .violations,
  ).toEqual([]);
  await page.screenshot({
    path: "../artifacts/scout-mobile.png",
    fullPage: true,
  });
  await page.getByRole("button", { name: "Open navigation" }).click();
  await page.keyboard.press("Escape");
  await expect(
    page.getByRole("button", { name: "Open navigation" }),
  ).toBeFocused();
  await page.getByRole("button", { name: "Open navigation" }).click();
  await page
    .getByRole("button", { name: "Documents & certificates", exact: true })
    .click();
  await expect(page.getByLabel("Your message to Scout")).toBeFocused();
  await page.getByLabel("Your message to Scout").fill("");
  expect(
    await page.evaluate(
      () => document.documentElement.scrollWidth <= window.innerWidth,
    ),
  ).toBeTruthy();
});

test("question to validated result, persistence, reload and deletion", async ({
  page,
  context,
}) => {
  const errors: string[] = [];
  page.on("pageerror", (e) => errors.push(e.message));
  await context.grantPermissions(["clipboard-read", "clipboard-write"]);
  await ready(page);
  await page
    .getByLabel("Your message to Scout")
    .fill("I lost my transfer certificate and need to return to school.");
  await page.getByRole("button", { name: "Send message" }).click();
  await expect(
    page.getByText(
      "Contact your previous school for a duplicate transfer certificate.",
    ),
  ).toBeVisible();
  await page
    .getByText("Documents & certificates · details & next steps")
    .click();
  await expect(
    page.getByText("Ask the school office about duplicate records."),
  ).toBeVisible();
  await page.getByRole("button", { name: "Copy response" }).click();
  await expect(
    page.getByRole("status").filter({ hasText: "Copied" }),
  ).toBeVisible();
  expect(await page.evaluate(() => navigator.clipboard.readText())).toContain(
    "Contact your previous school",
  );
  await page.reload();
  await expect(
    page.getByText(
      "Contact your previous school for a duplicate transfer certificate.",
    ),
  ).toBeVisible();
  await page.getByRole("button", { name: "New conversation" }).click();
  await expect(
    page.getByRole("heading", { name: "Big changes. Small steps forward." }),
  ).toBeVisible();
  await page
    .getByRole("button", {
      name: "I lost my transfer certificate and need to return to school.",
      exact: true,
    })
    .click();
  await expect(
    page.getByText(
      "Contact your previous school for a duplicate transfer certificate.",
    ),
  ).toBeVisible();
  await page.getByRole("button", { name: /^Delete conversation:/ }).click();
  await expect(
    page.getByRole("heading", { name: "Big changes. Small steps forward." }),
  ).toBeVisible();
  expect(errors).toEqual([]);
});

test("privacy dialog confirms removal of saved conversations", async ({
  page,
}) => {
  await ready(page);
  await page
    .getByLabel("Your message to Scout")
    .fill("Help me replace school records.");
  await page.getByRole("button", { name: "Send message" }).click();
  await expect(
    page.getByText(
      "Contact your previous school for a duplicate transfer certificate.",
    ),
  ).toBeVisible();
  await page.getByRole("button", { name: "About Scout", exact: true }).click();
  await expect(page.getByRole("dialog")).toBeVisible();
  expect(
    (await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa"]).analyze())
      .violations,
  ).toEqual([]);
  await page
    .getByRole("button", { name: "Delete all my data", exact: true })
    .click();
  await page
    .getByRole("button", { name: "Confirm delete all my data" })
    .click();
  await expect(page.getByRole("dialog")).not.toBeVisible();
  await expect(
    page.getByText("Your conversations will appear here."),
  ).toBeVisible();
});

test("rapid duplicate submits produce one API request", async ({ page }) => {
  await ready(page);
  let requests = 0;
  page.on("request", (request) => {
    if (request.url().endsWith("/api/chat")) requests += 1;
  });
  await page
    .getByLabel("Your message to Scout")
    .fill("Help with my school records.");
  await page.locator("form.composer").evaluate((form) => {
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );
  });
  await expect(
    page.getByText(
      "Contact your previous school for a duplicate transfer certificate.",
    ),
  ).toBeVisible();
  expect(requests).toBe(1);
});

test("missing provider setup is honest and disables sending", async ({
  page,
}) => {
  await page.route("**/api/session", (route) =>
    route.fulfill({ json: { ready: false, search_available: false } }),
  );
  await page.route("**/api/conversations", (route) =>
    route.fulfill({ json: [] }),
  );
  await page.goto("/");
  await expect(page.getByText("Setup needed")).toBeVisible();
  await expect(page.getByLabel("Your message to Scout")).toBeDisabled();
});

test("stop cancels work without presenting a fabricated answer", async ({
  page,
}) => {
  await ready(page);
  await page.getByLabel("Your message to Scout").fill("CANCEL_TEST");
  await page.getByRole("button", { name: "Send message" }).click();
  await page.getByRole("button", { name: "Stop request" }).click();
  await expect(page.getByRole("alert")).toContainText("request stopped");
  await expect(
    page.getByRole("article", { name: "Scout response" }),
  ).toHaveCount(0);
});

test("provider limits surface retry guidance and block immediate repeats", async ({
  page,
}) => {
  await ready(page);
  await page.getByLabel("Your message to Scout").fill("RATE_LIMIT_TEST");
  await page.getByRole("button", { name: "Send message" }).click();
  await expect(page.getByRole("alert")).toContainText("too many requests");
  await expect(
    page.getByRole("button", { name: /Try again in/ }),
  ).toBeDisabled();
  await expect(
    page.getByRole("button", { name: "Send message" }),
  ).toBeDisabled();
});
