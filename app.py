                        selected_links = recipe_links[recipe_links["recipe_id"] == rid]

                        for _, ingredient_row in selected_links.iterrows():
                            grocery_rows.append({
                                "Ingredient": ingredient_row["ingredient_name"],
                                "Quantity (g)": float(ingredient_row["quantity_g"]) * multiplier
                            })

                    if grocery_rows:

                        grocery = pd.DataFrame(grocery_rows).groupby("Ingredient", as_index=False)["Quantity (g)"].sum()
                        grocery["Quantity (g)"] = grocery["Quantity (g)"].round(0).astype(int)

                        st.caption("Combined ingredient quantities for the full seven-day plan. Pantry staples and water may already be available at home.")

                        st.dataframe(grocery, use_container_width=True, hide_index=True)

                        st.download_button(
                            "Download grocery list (CSV)",
                            data=grocery.to_csv(index=False).encode("utf-8"),
                            file_name="weekly_grocery_list.csv",
                            mime="text/csv",
                            key="weekly_grocery_download"
                        )

                    else:
                        st.info("No ingredient quantities are available for this plan.")

                st.download_button(
                    "Download 7-day meal plan (CSV)",
                    data=meal_plan.drop(columns=["Recipe ID"]).to_csv(index=False).encode("utf-8"),
                    file_name="personalized_7_day_recipe_meal_plan.csv",
                    mime="text/csv",
                )

                st.info(
                    "Nutrition is estimated from ingredient reference values and suggested portions. It is not a medical prescription. "
                    "Check labels and ingredient quantities, especially for allergies; consult a qualified dietitian for medical nutrition needs."
                )


    with reports_tab:
        # =================================================
        # HEALTH SUMMARY
        # =================================================

        st.markdown(
            f"""
            <section class="report-summary">
              <div class="report-summary-heading">
                <span class="report-summary-kicker">YOUR NUTRITION SNAPSHOT</span>
                <h3>Daily health summary</h3>
              </div>
              <div class="report-summary-grid">
                <div class="report-summary-item"><span>BMI</span><strong>{bmi}</strong></div>
                <div class="report-summary-item"><span>Water intake</span><strong>{water} L</strong></div>
                <div class="report-summary-item"><span>Protein requirement</span><strong>{protein} g</strong></div>
                <div class="report-summary-item"><span>Selected goal</span><strong>{goal}</strong></div>
                <div class="report-summary-item report-summary-wide"><span>Estimated daily calorie target</span><strong>{target_calories} kcal</strong></div>
              </div>
              <p class="report-summary-note">These values are estimates for general planning, not medical prescriptions.</p>
            </section>
            """,
            unsafe_allow_html=True,
        )

        # =================================================
        # DOWNLOAD BUTTONS FOR RECOMMENDATIONS
        # =================================================

        csv = foods.to_csv(index=False)

        pdf_rec_bytes = generate_pdf_report(
            goal, bmi, water, protein, bmr, tdee, foods, target_calories
        )

        col_rec1, col_rec2 = st.columns(2)

        with col_rec1:
            st.download_button(
                label="📥 Download Recommendations (CSV)",
                data=csv,
                file_name="diet_recommendations.csv",
                mime="text/csv"
            )

        with col_rec2:
            st.download_button(
                label="📄 Download Recommendations (PDF)",
                data=pdf_rec_bytes,
                file_name="diet_recommendations.pdf",
                mime="application/pdf"
            )


# =====================================================
# FOOTER
# =====================================================

st.markdown("---")         
