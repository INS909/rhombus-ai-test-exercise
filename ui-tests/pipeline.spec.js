const { test, expect } = require('@playwright/test');
const path = require('path');

test.use({ storageState: 'auth.json' });
test.setTimeout(300000); // 5 minute timeout for the whole test

test('AI Pipeline Flow - upload CSV and run pipeline', async ({ page }) => {
  // Step 1 - Navigate to dashboard
  await page.goto('https://rhombusai.com');
  await expect(page.locator('text=New Project')).toBeVisible({ timeout: 15000 });

  // Step 2 - Click New Project button
  await page.click('text=New Project');

  // Step 3 - Fill in project name and create it
  await expect(page.locator('text=Create New Project')).toBeVisible({ timeout: 5000 });
  const projectName = `Test Pipeline ${Date.now()}`;
  await page.fill('input[placeholder="Enter project name"]', projectName);
  await page.locator('dialog button:has-text("Create"), [role="dialog"] button:has-text("Create")').click();

  // Wait for workflow canvas to load
  await expect(page.locator('button:has-text("Run Pipeline")')).toBeVisible({ timeout: 15000 });

  // Step 4 - Click + button and select Add new file from menu
  await page.locator('aside button').first().click();
  await expect(page.locator('text=Add new file')).toBeVisible({ timeout: 5000 });
  await page.locator('text=Add new file').click();

  // Step 4b - Upload CSV via the Add New File dialog hidden input
  await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 });
  await page.getByRole('dialog').locator('input[type="file"]').setInputFiles(
    path.join(__dirname, '../data-validation/test-data.csv'),
    { force: true }
  );

  // Wait for Upload button to enable then click it
  await expect(page.locator('button:has-text("Upload")')).toBeEnabled({ timeout: 10000 });
  await page.locator('button:has-text("Upload")').click();

  // Step 5 - Type the AI prompt in the chat textarea
  await expect(page.locator('textarea').first()).toBeVisible({ timeout: 10000 });
  await page.locator('textarea').first().fill('Clean this data - standardise name casing, fix date formats, remove extra whitespace');

  // Step 6 - Click the send button to submit prompt to AI
  await page.locator('aside').locator('button').last().click();

  // Step 7 - Wait for AI to finish building the pipeline
  await expect(page.locator('[data-testid="run-pipeline"]')).toBeEnabled({ timeout: 180000 });
  await page.waitForTimeout(2000);

  // Step 8 - Run the pipeline
  await page.locator('[data-testid="run-pipeline"]').click({ force: true });

  // Step 9 - Wait for pipeline execution to complete
  await expect(
    page.locator('text=Pipeline execution completed successfully')
  ).toBeVisible({ timeout: 120000 });

  console.log('✅ Pipeline completed successfully!');
});