import type { Meta, StoryObj } from "@storybook/vue3";
import { provide, ref, computed } from "vue";
import Separator from "../../../core_components/layout/CoreSeparator.vue";
import injectionKeys from "../../../injectionKeys";
import "remixicon/fonts/remixicon.css";
import { generateCore } from "../../fakeCore";

// More on how to set up stories at: https://storybook.js.org/docs/writing-stories
const meta = {
	title: "core-components/layout/Separator",
	component: Separator,
	// This component will have an automatically generated docsPage entry: https://storybook.js.org/docs/writing-docs/autodocs
	tags: ["autodocs"],
	argTypes: {
		separatorColor: { control: "text" },
		cssClasses: { control: "text" },
	},
} satisfies Meta<typeof Separator>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Sample: Story = {
	render: (args) => ({
		components: { Separator },
		setup() {
			const ss = generateCore();
			args.rootStyle = computed(() => {
				return {
					"--accentColor": "#29cf00",
					"--buttonColor": "#ffffff",
					"--emptinessColor": "#e9eef1",
					"--separatorColor": "rgba(0, 0, 0, 0.07)",
					"--primaryTextColor": "#202829",
					"--buttonTextColor": "#202829",
					"--secondaryTextColor": "#5d7275",
					"--containerBackgroundColor": "#ffffff",
				};
			});
			provide(injectionKeys.evaluatedFields, {
				separatorColor: computed(() => args.separatorColor),
				cssClasses: computed(() => args.cssClasses),
			});
			provide(injectionKeys.isDisabled, ref(false));
			provide(injectionKeys.core, ss as any);
			return { args };
		},
		template:
			'<Separator :style="args.rootStyle" :prop-name="args.propName" />',
	}),
};
	